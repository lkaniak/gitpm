import api, { HttpMethods } from ".";

const controllerUrl = '/process';

interface GenerateProcessProps {
  logName: string,
  params: [string],
}

interface DownloadProcessProps {
  logName: string,
}

export async function generateLog(payload:GenerateProcessProps) {
  return await api({ method: HttpMethods.POST, url: `${controllerUrl}/generate_process`, data: payload });
}

export async function downloadLog(payload:DownloadProcessProps) {
  return await api({ method: HttpMethods.POST, url: `${controllerUrl}/download`, data: payload });
}
