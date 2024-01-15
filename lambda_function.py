import json
import boto3
import os
import uuid
import base64
import pathlib
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: gv_uploadsong**")
    

    config_file = 'config.ini'
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
    
    configur = ConfigParser()
    configur.read(config_file) 
    
    
    s3_profile = 's3readwrite'
    boto3.setup_default_session(profile_name=s3_profile)
    
    bucketname = configur.get('s3', 'bucket_name')
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketname)
    
    
    rds_endpoint = configur.get('rds', 'endpoint')
    rds_portnum = int(configur.get('rds', 'port_number'))
    rds_username = configur.get('rds', 'user_name')
    rds_pwd = configur.get('rds', 'user_pwd')
    rds_dbname = configur.get('rds', 'db_name')


    #
    # the user has sent us two parameters:
    #  1. the name of the song
    #  2. the artist of the song
    #  3. the album the song is in
    #  4. the original filename of the song
    #  5. raw file data in base64 encoded string
    #
    # The parameters are coming through web server 
    # (or API Gateway) in the body of the request
    # in JSON format.
    #
    print("**Accessing request body**")
    
    if "body" not in event:
      raise Exception("event has no body")
      
    body = json.loads(event["body"]) # parse the json
    
    if "songname" not in body:
      raise Exception("event has a body but no songname")
    if "artist" not in body:
      raise Exception("event has a body but no artist")
    if "album" not in body:
      raise Exception("event has a body but no album")
    if "og_filename" not in body:
      raise Exception("event has a body but no og_filename")
    if "data" not in body:
      raise Exception("event has a body but no data")


    songname = body["songname"]
    artist = body["artist"]
    album = body["album"]
    og_filename = body["og_filename"]
    datastr = body["data"]
    
    print("songname:", songname)
    print("artist:", artist)
    print("album:", album)
    print("og_filename:", og_filename)
    print("datastr (first 10 chars):", datastr[0:10])

    #
    # open connection to the database:
    #
    print("**Opening connection**")
    
    dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
  
    base64_bytes = datastr.encode()        # string -> base64 bytes
    bytes = base64.b64decode(base64_bytes) # base64 bytes -> raw bytes
    
    #
    # write raw bytes to local filesystem for upload:
    #
    print("**Writing local data file**")
    
    local_filename = "/tmp/data.mp3"
    
    outfile = open(local_filename, "wb")
    outfile.write(bytes)
    outfile.close()
    
    #
    # generate unique filename in preparation for the S3 upload:
    #
    print("**Uploading local file to S3**")
    
    basename = pathlib.Path(og_filename).stem
    extension = pathlib.Path(og_filename).suffix
    
    if extension != ".mp3" : 
      raise Exception("expecting og_filename to have .mp3 extension")
    
    bucketkey = "groovevault/" + basename + "-" + str(uuid.uuid4()) + ".mp3"
    
    print("S3 bucketkey:", bucketkey)
    
    #
    # add a jobs record to the database BEFORE we upload, just in case
    # the compute function is triggered faster than we can update the
    # database:
    #
    print("**Adding jobs row to database**")
    
    sql = """
      INSERT INTO songs(songname, artist, album, originalsongfile, songfilekey)
                  VALUES(%s, %s, %s, %s, %s);
    """
    
    datatier.perform_action(dbConn, sql, [songname, artist, album, og_filename, bucketkey])
    
    #
    # grab the songid that was auto-generated by mysql:
    #
    sql = "SELECT LAST_INSERT_ID();"
    
    row = datatier.retrieve_one_row(dbConn, sql)
    
    songid = row[0]
    
    print("songid:", songid)
    
    #
    # finally, upload to S3:
    #
    print("**Uploading data file to S3**")

    bucket.upload_file(local_filename, 
                       bucketkey, 
                       ExtraArgs={
                         'ACL': 'public-read',
                         'ContentType': 'audio/mpeg'
                       })

    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
    print("**DONE, returning songid**")
    
    return {
      'statusCode': 200,
      'body': json.dumps(str(songid))
    }
    
  except Exception as err:
    print("**ERROR**")
    print(str(err))
    
    return {
      'statusCode': 400,
      'body': json.dumps(str(err))
    }
