#!/bin/bash

ISSUE_TITLE="$1"
ISSUE_BODY="$2"

cat <<EOF
Clasifica la siguiente incidencia de GitHub. Devuelve la respuesta en formato JSON con las claves 'label' (ej. 'bug', 'feature', 'documentation', 'enhancement') y 'priority' (ej. 'low', 'medium', 'high', 'critical').

Título: ${ISSUE_TITLE}
Cuerpo: ${ISSUE_BODY}
EOF