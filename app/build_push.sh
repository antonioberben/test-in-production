docker build -f Dockerfile_app1 --push -t antonioberben/baggage-demo-app1:0.9 .
docker build -f Dockerfile_app2 --push -t antonioberben/baggage-demo-app2:0.9 .
docker build -f Dockerfile_app3 --push -t antonioberben/baggage-demo-app3:0.9 .
docker build -f Dockerfile_app3_new_version --push -t antonioberben/baggage-demo-app3:0.9-new-version .

