import HelpOutline from "@suid/icons-material/HelpOutline";
import { IconButton } from "@suid/material";
import HelperDrawer from "./drawer"

export default function Helper() {
  return (
    <>
      <HelperDrawer />
      <IconButton color="secondary" aria-label="help">
        <HelpOutline />
      </IconButton>
    </>
  );
}