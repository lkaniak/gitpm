


import Clear from "@suid/icons-material/Clear";
import Search from "@suid/icons-material/Search";
import Code from "@suid/icons-material/Code";
import { InputAdornment, TextField,  IconButton, CircularProgress } from "@suid/material";
import { createSignal, createResource, createEffect } from "solid-js";
import { obtainCommits } from "~/api/repositories";


export const [commits, setCommits] = createSignal();

export default function RepoSearch() {
  const [input, setInput] = createSignal("");
  const [sanitizedInput, setSanitizedInput] = createSignal("");
  const [loading, setLoading] = createSignal(false);
  const [error, setError] = createSignal("");
  const [repoCommitsResource] = createResource({ repoUrl: sanitizedInput() }, obtainCommits);

  const sanitize = (s:string):string => {
    let validGithubUrl = s;
    if (!s.includes("https://github.com")) {
      validGithubUrl = "https://github.com/" + s;
    }
    return validGithubUrl;
  }

  createEffect(() => {
    const repoCommits = repoCommitsResource();
    if (repoCommits) {
      setCommits(repoCommits);
    } else if (repoCommitsResource.error) {
      setError("Error");
    }
    if (repoCommitsResource.loading) {
      setLoading(true);
    } else {
      setLoading(false);
    }
  });


  return (
    <>
      <TextField
        label="Repositorio"
        error={error().length > 0}
        helperText={error()}
        id="outlined-start-adornment"
        sx={{
          m: 1,
          width: "25ch",
        }}
        value={input()}
        onChange={(event, value) => {
          setInput(value);
        }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Code />
            </InputAdornment>
          ),
          endAdornment: (
            input()
              ? (<InputAdornment position="end">
                {loading()
                  ? <CircularProgress />
                  : (<IconButton onClick={() => setInput("")}>
                      <Clear />
                    </IconButton>)
                }
                </InputAdornment>)
              : (<></>)
          ),
        }}
      />
      {input() ?
        (<IconButton onClick={() => setSanitizedInput(sanitize(input()))}>
          <Search />
        </IconButton>) : null
      }
    </>
  );
}