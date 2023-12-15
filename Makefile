VENV ?= .venv
MODULE=ical_generator
ICAL=dist/qld_school_term_2024.ical

all: ical

dist/%.ical: %.yaml
	${VENV}/bin/python -m ${MODULE} -o $@ $<

ical: ${ICAL} 

fmt:
	black -l100 ${MODULE}/
	ruff --line-length=100 --select=E,F,I --fix ${MODULE}/

show: ${ICAL}
	open $<

clean:
	-rm -f ${ICAL}

rebuild: clean ical

netlify:
	python3 -m venv ${VENV}
	${VENV}/bin/python -m pip install -U pip
	${VENV}/bin/python -m pip install -r reqs.txt
	${MAKE}	rebuild
