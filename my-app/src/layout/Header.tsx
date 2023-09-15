import MenuIcon from "@suid/icons-material/Menu";
import {
  AppBar,
  Box,
  Button,
  IconButton,
  Toolbar,
  Typography,
} from "@suid/material";
import Helper from "~/core/components/helper";
import Options from "~/core/components/options";

export default function Header() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Options />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Gitpm
          </Typography>
          <Helper />
        </Toolbar>
      </AppBar>
    </Box>
  );
}