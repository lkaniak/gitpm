import api, { HttpMethods } from ".";

const controllerUrl = '/repositories/external';

interface ObtainCommitsProps {
  repoUrl: string
}

export async function obtainCommits(payload:ObtainCommitsProps) {
  return await api({ method: HttpMethods.POST, url: `${controllerUrl}/get_commits`, data: payload })
}

export async function downloadRepository(payload:ObtainCommitsProps) {
  return await api({ method: HttpMethods.POST, url: `${controllerUrl}/download`, data: payload })
}
