{{- define "mariadb.name" -}}
{{- printf "mariadb" }}
{{- end }}

{{- define "mariadb.fullname" -}}
{{- $componentName := include "mariadb.name" .  }}
{{- if .Values.mariadb.fullnameOverride }}
{{- .Values.mariadb.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s-v2" .Release.Name $componentName | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "mariadb.labels" -}}
{{ include "mariadb.selectorLabels" . }}
{{- if .Values.global.tag }}
app.kubernetes.io/image-version: {{ .Values.global.tag | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/short-name: {{ include "mariadb.name" . }}
{{- end }}

{{- define "mariadb.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mariadb.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}