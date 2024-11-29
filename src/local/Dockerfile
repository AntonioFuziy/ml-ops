FROM public.ecr.aws/lambda/python:3.10

RUN yum install -y libstdc++ cmake gcc-c++ && \
    yum clean all && \
    rm -rf /var/cache/yum
    
COPY requirements.txt ${LAMBDA_TASK_ROOT}

COPY src/handler.py ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD [ "lambdas.${LAMBDA_NAME}.handler" ]