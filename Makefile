APP_NAME?=$(shell pwd | xargs basename)

clean-up:
ifneq ($(shell docker ps --filter "name=${APP_NAME}" -q 2> /dev/null | wc -l | bc), 0)
	@echo "\e[1m\033[33mRemoving containers\e[0m"
	@docker ps --filter "name=${APP_NAME}" -q | xargs docker rm -f
endif

python:
	@echo "\e[1m\033[33mDebug mode\e[0m"
	@$(eval APP_DIR:=/go/src/github.com/victorabarros/${APP_NAME})
	@docker run -it -v $(shell pwd):${APP_DIR} -w ${APP_DIR} \
        --env-file app/.env \
		-p 5001:5000 --name ${APP_NAME}-python python:3.8 bash

ip:
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${APP_NAME}

ip-all:
	@docker ps -q | xargs docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
