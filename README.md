# Enzo API Access via Kubernetes

Access the Enzo API after I initiated the port-forward service/pr-enzo 8080:4108 from kubernetics

Access the ENZO API
Based on the instruction and the example received: 
curl -v \    
-H "Authorization: Bearer ${JWT}" \    
-H 'Content-Type: application/json' \    
-H 'Accept: application/json' \    
-H "CallTreeId: $(uuidgen)" \    
--data '{"customerId":"27611005291","store":"529", "fulfilmentType": "FSD", "articles":[{"mgb":"1001001"}]}' \    'http://localhost:4108/list/de'

For the ES country, changed the http://localhost:4108/list/de in http://localhost:4108/list/es

IDAM-JWT

For the secret key, I utilized the idam-jwt, which I initialized when you logged in to the Metro application. When you log into the Metro application, the idam-jwt file is generated dynamically. 