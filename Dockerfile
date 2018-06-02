FROM python:3.6

ENV APP_USER dprsale
ENV APP_ROOT /dprsale
RUN mkdir /dprsale
RUN groupadd -r ${APP_USER} \
    && useradd -r -m \
    --home-dir ${APP_ROOT} \
    -s /usr/sbin/nologin \
    -g ${APP_USER} ${APP_USER}

WORKDIR ${APP_ROOT}

COPY . ${APP_ROOT}


# ADD . ${APP_ROOT}

RUN pip install -r requirements.txt

#RUN mkdir uploads

#RUN chmod -R 777 uploads

#RUN mkdir static

RUN chmod -R 777 static

RUN python manage.py collectstatic --noinput

USER ${APP_USER}
