import { DrawerProps } from "@suid/material/Drawer/DrawerProps";
import { toggleDrawerHOC, DrawerHOCstate, DrawerHOC } from "~/shared/components/Drawer";
import FormOptions from "../form";

export const toggleDrawerOptions = (e) => toggleDrawerHOC("options", !DrawerHOCstate["options"], DrawerHOCstate)(e);

export default function OptionsDrawer(props:DrawerProps) {

  const anchorPos = 'left'

  return (
    <DrawerHOC
      drawer="options"
      anchor={anchorPos}
      open={DrawerHOCstate["options"]}
      sx={{ zIndex: 9999 }}
      onClose={toggleDrawerOptions}
    >
      <FormOptions />
    </DrawerHOC>
  );
}