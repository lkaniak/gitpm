import {
  Drawer,
} from "@suid/material";

import { createMutable } from "solid-js/store";
import { FlowComponent, FlowProps } from "solid-js";
import { DrawerProps } from "@suid/material/Drawer";

type AppDrawers = { drawer: "options" | "help" };

export type DrawerCompProps = DrawerProps & FlowProps & AppDrawers;
export type DrawersStates = NonNullable<AppDrawers["drawer"]>;

export const toggleDrawerHOC =
  (drawer: DrawersStates, open: boolean, state: { [K in DrawersStates]: boolean; }) => (event: MouseEvent | KeyboardEvent) => {
    console.log('\n#############teste');
    if (event.type === "keydown") {
      const keyboardEvent = event as KeyboardEvent;
      if (keyboardEvent.key === "Tab" || keyboardEvent.key === "Shift")
        return;
    }
    state[drawer] = open;
  };

export const DrawerHOCstate = createMutable<{
    [K in DrawersStates]: boolean;
  }>({
    options: false,
    help: false,
  });

export const DrawerHOC: FlowComponent<DrawerCompProps> = (props) => {

  return (
    <Drawer
      anchor={props.anchor ?? "bottom"}
      open={DrawerHOCstate[props.drawer]}
      sx={{ zIndex: 9999 }}
      onClose={toggleDrawerHOC(props.drawer, false, DrawerHOCstate)}
    >
      {props.children}
    </Drawer>
  );
}