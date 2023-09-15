import SettingsApplications from "@suid/icons-material/SettingsApplications";
import { IconButton } from "@suid/material";
import OptionsDrawer from "./drawer"

export default function Options() {
  return (
    <>
      <OptionsDrawer />
      <IconButton color="secondary" aria-label="settings">
        <SettingsApplications />
      </IconButton>
    </>
  );
}