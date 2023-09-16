import Settings from "@suid/icons-material/Settings";
import { IconButton } from "@suid/material";
import OptionsDrawer, { toggleDrawerOptions } from "./drawer"

export default function Options() {

  return (
    <>
      <OptionsDrawer />
      <IconButton color="secondary" aria-label="settings" onClick={(e) => toggleDrawerOptions(e)}>
        <Settings />
      </IconButton>
    </>
  );
}