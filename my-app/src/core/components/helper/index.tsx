import HelpOutline from "@suid/icons-material/HelpOutline";
import { IconButton } from "@suid/material";
import HelperDrawer, { toggleDrawerHelp } from "./drawer"

export default function Helper() {
  return (
    <>
      <HelperDrawer />
      <IconButton color="secondary" aria-label="help" onClick={() => toggleDrawerHelp}>
        <HelpOutline />
      </IconButton>
    </>
  );
}