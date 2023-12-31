VENV ?= .venv/bin/
MODULE=ical_generator
ICAL=dist/qld_school_term_2024.ical

all: ical

dist/%.ical: %.yaml
	${VENV}python -m ${MODULE} -o $@ $<

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
	python -V
	pip install -U pip
	pip --version
	pip install --index-url=https://pypi.org/project/simple/ -r reqs.txt
	${MAKE}	rebuild
