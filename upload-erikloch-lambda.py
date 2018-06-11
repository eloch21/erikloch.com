import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:624886297825:deployErikLochTopic')

    try:
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

        print "Job Done!"
        topic.publish(Subject="erikloch.com deployed", Message="erikloch.com deployed successfully")
    except:
        topic.publish(Subject="erikloch.com deployed Failed", Message="erikloch.com was not deployed successfully")
        raise
