django-s3-proxy
===============

A Django app for linking static apps hosted on Amazon S3 to URLs in a standard Django project.

With ``django-s3-proxy``, you can use a subdirectory on your domain like ``doordash.com/my-app`` to access a Static Website hosted in an Amazon S3 bucket by forwarding resource requests to their corresponding file in S3.

## About
At DoorDash, many of our internal apps are written as single page Angular apps. Our main site is built using the Django framework, and our static assets are automatically uploaded and hosted on S3 using the great [Boto](https://github.com/boto/boto) and [django-storages](http://django-storages.readthedocs.org/en/latest/) extensions. 

For ease of development, these internal apps are hosted in their own Amazon S3 bucket independent of our Django app, and often have their own repository. We find this approach has a number of benefits:

* We can develop and deploy our static apps independently of our Django deploys
* We can use tools like Bower, Yeoman, and Grunt without complicated configuration to work in the same repo as our Django app
* It forces us to develop and use a solid internal RESTful API

While [hosting static apps](http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html) on S3 is generally very solid, one major disadvantage is that Static Websites have their own region-specific website endpoint for each bucket, which can only be linked to our ``doordash.com`` URL config through DNS, e.g. adding a CNAME record from ``my-app.doordash.com`` to ``my-app.doordash.com.s3-website-us-west-1.amazonaws.com``.

``django-s3-proxy`` allows us to map a subdirectory like ``doordash.com/my-app`` to its corresponding Static Webite in an Amazon S3 bucket by proxying requests, enabling us to host our static apps wherever we want to.
