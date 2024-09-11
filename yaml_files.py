# default_deployment_content = """
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: {job_name}
# spec:
#   replicas: 1
#   selector:
#     matchLabels:
#       app: {job_name}
#   template:
#     metadata:
#       labels:
#         app: {job_name}
#     spec:
#       containers:
#       - name: {job_name}
#         image: {image_name}
#         resources:
#           limits:
#             memory: "128Mi"
#             cpu: "500m"
# """

default_service_content = """
apiVersion: v1
kind: Service
metadata:
  name: {job_name}
spec:
  selector:
    app: {job_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
"""

default_deployment_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {job_name}
  namespace: TEST-PROJECT
  labels:
    app: TEST-PROJECT
spec:
  selector:
    matchLabels:
      app: TEST-PROJECT
  replicas:
  strategy: 
    type:
    rollingUpdate:
  template:
    metadata:
      labels:
        app: TEST-PROJECT
    spec:
      containers:
      - name: {job_name}
        image: {image_name}
        resources:
          limits:
            cpu: 128m
            memory: 500Mi
          requests:
            cpu: 20m
            memory: 100Mi  
        envFrom:
        - secretRef:
            name: {job_name}
        imagePullPolicy:
        ports:
        - containerPort:
      nodeSelector:
        allowed:
      tolerations:
      - effect:
        key:
        operator:
        value:         
      imagePullSecrets:
        - name:
---

apiVersion:
kind: Service
metadata:
  name: {job_name}
  namespace: TEST-PROJECT
spec:
  selector:
    app: TEST-PROJECT
  type:
  ports:
  - protocol:
    port:
    targetPort:
---
apiVersion:
kind:
metadata:
  name: {job_name}
  namespace: TEST-PROJECT
spec:
  scaleTargetRef:
    apiVersion:
    kind: Deployment
    name: {job_name}
  minReplicas:
  maxReplicas:
  metrics:
  - type:
    resource:
      name:
      target:
        type:
        averageValue:
  - type:
    resource:
      name:
      target:
        type:
        averageValue:    
  behavior:
    scaleDown:
      stabilizationWindowSeconds:
      policies:
      - type:
        value:
        periodSeconds:
      selectPolicy:
"""