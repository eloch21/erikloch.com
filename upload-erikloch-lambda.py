import boto3
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3')

erikloch_bucket = s3.Bucket('erikloch.com')
build_bucket = s3.Bucket('build.erikloch.com')

portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        erikloch_bucket.upload_fileobj(obj, nm,
        ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        erikloch_bucket.Object(nm).Acl().put(ACL='public-read')
