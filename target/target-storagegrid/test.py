import requests
import html2text
import pdfkit
import boto3
import boto3.session
import urllib3
import ssl
import urllib3
urllib3.disable_warnings()


def main():
	url = 'https://www.singer.io/tap/github'
	filename = 'file5.txt'
	bucketname = 'test-bucket-store1'

	html_content = requests.get(url)
	rendered_content = html2text.html2text(html_content.text)

	file = open(filename, 'w', encoding="utf-8")
	file.write(rendered_content)
	file.close()

	session = boto3.session.Session(profile_name='default')
	endpoint = 'https://113.29.246.178:8082/'
	s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify=False)

	file = s3.Object(bucketname, filename).put(Body=rendered_content)


if __name__ == '__main__':
    main()
   