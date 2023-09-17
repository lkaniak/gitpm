import { Box, Grid, IconButton, TextField, Typography } from "@suid/material";
import { For, createEffect, createSignal } from "solid-js";
import ArrowForwardIos from "@suid/icons-material/ArrowForwardIos";
import Close from "@suid/icons-material/Close";

type ParameterView = {
  id: number
  value: string
}

const [parameters, setParameters] = createSignal<ParameterView[]>([]);

export function addParameter() {
  setParameters((prev) => {
    let newParameter:ParameterView = {
      id: 0,
      value: ""
    }
    const prevIds = prev.map(p => p.id).sort((a, b) => a - b);
    let curr = 0;
    let next = curr + 1;
    while (prevIds[next] - prevIds[curr] === 1) {
      curr += 1
      next += 1
    }
    if (!prevIds[curr] || Number.isNaN(prevIds[curr])) {
      newParameter.id = prev.length + 1
    } else {
      newParameter.id = prevIds[curr] + 1
    }

    return [...prev, newParameter]
  });
}

function removeParameterById(id:number) {
  setParameters((prev) => prev.filter(p => p.id !== id));
}

export function CustomParameters() {
  return (
    <For each={parameters()}>{p =>
      <Grid container item flexWrap="nowrap" alignItems="center" >
        <Grid item>
          <IconButton  color="secondary" aria-label="help-options">
            <Close onClick={() => removeParameterById(p.id)} />
          </IconButton>
        </Grid>
        <Grid item flexGrow={1}>
          <Typography variant="body1" component="div">
            Parametro {p.id}
          </Typography>
        </Grid>
        <Grid item>
          <TextField
            id="log-name"
            label={`Parametro ${p.id}`}
            variant="standard"
            size="small"
            sx={{ width: 175, paddingBottom: 1 }}
          />
        </Grid>
      </Grid>
    }</For>
  )
}