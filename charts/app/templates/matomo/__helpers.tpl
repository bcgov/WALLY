{{- define "matomo.name" -}}
{{- printf "matomo" }}
{{- end }}

{{- define "matomo.fullname" -}}
{{- $componentName := include "matomo.name" .  }}
{{- if .Values.matomo.fullnameOverride }}
{{- .Values.matomo.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s-v2" .Release.Name $componentName | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "matomo.labels" -}}
{{ include "matomo.selectorLabels" . }}
{{- if .Values.global.tag }}
app.kubernetes.io/image-version: {{ .Values.global.tag | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/short-name: {{ include "matomo.name" . }}
{{- end }}

{{- define "matomo.selectorLabels" -}}
app.kubernetes.io/name: {{ include "matomo.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}