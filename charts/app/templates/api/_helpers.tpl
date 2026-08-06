{{- define "backend.name" -}}
{{- printf "backend" }}
{{- end }}

{{- define "backend.fullname" -}}
{{- $componentName := include "backend.name" .  }}
{{- if .Values.backend.fullnameOverride }}
{{- .Values.backend.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $componentName | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "backend.labels" -}}
{{ include "backend.selectorLabels" . }}
{{- if .Values.global.tag }}
app.kubernetes.io/image-version: {{ .Values.global.tag | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/short-name: {{ include "backend.name" . }}
{{- end }}

{{- define "backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Secrets
*/}}
{{- define "backend.pgSecretName" -}}
{{- printf "%s-pguser-%s" .Values.global.databaseAlias .Values.global.config.databaseUser -}}
{{- end }}

