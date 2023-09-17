import HelpOutline from "@suid/icons-material/HelpOutline";
import Description from "@suid/icons-material/Description";
import People from "@suid/icons-material/People";
import DataObject from "@suid/icons-material/DataObject";
import Add from "@suid/icons-material/Add";
import { Box, Button, Divider, Grid, IconButton, TextField, Typography } from "@suid/material";
import { toggleDrawerOptions } from "./drawer";
import { CustomParameters, addParameter } from "./customParameter";

export default function FormOptions() {

  return (
    <Box
      sx={{ width: 350, height: '100%' }}
      role="presentation"
      onKeyDown={toggleDrawerOptions}
    >
      <Grid container justifyContent="space-between" sx={{ height: '100%' }} direction="column">
        <Grid container item direction="row">
          <Grid container item sx={{ padding: 1 }} justifyContent="space-between" alignItems="center">
            <Grid item>
              <Typography variant="h6" component="div" sx={{ width: 75 }}>
                Opções
              </Typography>
            </Grid>
            <Grid item>
              <IconButton color="secondary" aria-label="help-options">
                <HelpOutline />
              </IconButton>
            </Grid>
          </Grid>
          <Divider />
          <Grid container item sx={{ padding: 1 }} justifyContent="space-around" alignItems="center" columns={2}>
            <Grid item >
              <Button variant="contained" color="success" aria-label="help">
                Gerar Log
              </Button>
            </Grid>
            <Grid item>
              <Button variant="contained" color="success" aria-label="help">
                Gerar Processo
              </Button>
            </Grid>
          </Grid>
          <Grid container item sx={{ padding: 1 }} columns={1} rowSpacing={1.5}>
            <Grid container item flexWrap="nowrap" alignItems="end">
              <Grid item>
                <IconButton color="secondary" aria-label="help-options">
                  <Description />
                </IconButton>
              </Grid>
              <Grid item flexGrow={1}>
                <TextField
                  id="log-name"
                  label="Nome do log"
                  variant="standard"
                  size="small"
                  sx={{ width: '100%' }}
                />
              </Grid>
            </Grid>
            <Grid container item flexWrap="nowrap" alignItems="end">
              <Grid item>
                <IconButton color="secondary" aria-label="help-options">
                  <People />
                </IconButton>
              </Grid>
              <Grid item flexGrow={1}>
                <TextField
                  id="standard-small"
                  label="Commits por pessoa"
                  variant="standard"
                  size="small"
                  sx={{ width: '100%' }}
                />
              </Grid>
            </Grid>
            <Grid container item flexWrap="nowrap" alignItems="center" >
              <Grid item>
                <IconButton color="secondary" aria-label="help-options">
                  <DataObject />
                </IconButton>
              </Grid>
              <Grid item flexGrow={1}>
                <Typography variant="body1" component="div">
                  Adicionar Parametros
                </Typography>
              </Grid>
              <Grid item>
                <IconButton color="secondary" aria-label="help-options" onClick={() => addParameter()}>
                  <Add />
                </IconButton>
              </Grid>
            </Grid>
          </Grid>
          <Grid container item sx={{ padding: 1 }} columns={1} rowSpacing={1}>
            <CustomParameters />
          </Grid>
        </Grid>
        <Grid container item direction="row">
            <Typography variant="subtitle1" component="div" sx={{ padding: 3 }}>
              Made by <a href="https://github.com/lkaniak">lkaniak</a>.
            </Typography>
        </Grid>
      </Grid>
    </Box>
  );
}