{{- define "minio.name" -}}
{{- printf "minio" }}
{{- end }}

{{- define "minio.fullname" -}}
{{- $componentName := include "minio.name" .  }}
{{- if .Values.minio.fullnameOverride }}
{{- .Values.minio.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $componentName | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "minio.labels" -}}
{{ include "minio.selectorLabels" . }}
{{- if .Values.global.tag }}
app.kubernetes.io/image-version: {{ .Values.global.tag | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/short-name: {{ include "minio.name" . }}
{{- end }}

{{- define "minio.selectorLabels" -}}
app.kubernetes.io/name: {{ include "minio.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}