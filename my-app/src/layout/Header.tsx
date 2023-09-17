import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Grid,
} from "@suid/material";

import Export from "~/core/components/export";
import Helper from "~/core/components/helper";
import Options from "~/core/components/options";
import RepoSearch from "~/core/components/repoSearch";

export default function Header() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ width: 75 }}>
            Gitpm
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'flex' } }}>
            <RepoSearch />
          </Box>
          <Export />
          <Options />
          <Helper />
        </Toolbar>
      </AppBar>
    </Box>
  );
}