import api, { HttpMethods } from ".";

const controllerUrl = '/eventlog';

interface GenerateLogProps {
  url: string,
  minCommits: Number,
  logName: string,
}

interface DownloadLogProps {
  logName: string,
}

export async function generateLog(payload:GenerateLogProps) {
  return await api({ method: HttpMethods.POST, url: `${controllerUrl}/generate_log`, data: payload });
}

export async function downloadLog(payload:DownloadLogProps) {
  return await api({ method: HttpMethods.POST, url: `${controllerUrl}/download`, data: payload });
}
