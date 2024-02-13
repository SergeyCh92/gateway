FROM python:3.11.1

WORKDIR /usr/app

COPY ./gateway_service /usr/app/gateway_service
COPY ./requirements.txt /usr/app
COPY ./libs /usr/app/libs

RUN pip install --no-cache-dir --upgrade -r /usr/app/requirements.txt
RUN pip install /usr/app/libs/common_rabbit-1.0.0-py3-none-any.whl  \
    /usr/app/libs/common_core-1.0.0-py3-none-any.whl \
    /usr/app/libs/ipr-0.1.0-py3-none-any.whl \
    /usr/app/libs/vlp-0.1.0-py3-none-any.whl \
    /usr/app/libs/nodal_analysis-0.1.0-py3-none-any.whl

ENV PYTHONPATH "${PYTHONPATH}:/usr/app"