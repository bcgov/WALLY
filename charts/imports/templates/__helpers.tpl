{{/*
Expand the name of the chart / release, used for naming resources.
*/}}
{{- define "wally-importer.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{/*
Secrets
*/}}
{{- define "backend.PGSuperUser" -}}
{{- printf "%s-pguser-%s" .Values.global.databaseAlias .Values.global.databaseSuperUser}}
{{- end }}

{{- define "backend.PGApplicationUser" -}}
{{- printf "%s-pguser-%s" .Values.global.databaseAlias .Values.global.databaseApplicationUser -}}
{{- end }}