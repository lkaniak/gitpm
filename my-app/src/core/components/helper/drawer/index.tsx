import MailIcon from "@suid/icons-material/Mail";
import InboxIcon from "@suid/icons-material/MoveToInbox";
import {
  Box,
  Divider,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@suid/material";
import { DrawerProps } from "@suid/material/Drawer";
import { toggleDrawerHOC, DrawerHOCstate, DrawerHOC } from "~/shared/components/Drawer";


export default function HelperDrawer(props:DrawerProps) {

  const anchorPos = 'bottom'

  const toggleDrawer = () => toggleDrawerHOC(anchorPos, DrawerHOCstate[anchorPos], DrawerHOCstate)

  const list = () => (
    <Box
      sx={{ width: "auto" }}
      role="presentation"
      onClick={toggleDrawer}
      onKeyDown={toggleDrawer}
    >
      <List>
        {["Inbox", "Starred", "Send email", "Drafts"].map((text, index) => (
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        {["All mail", "Trash", "Spam"].map((text, index) => (
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <DrawerHOC
      anchor={anchorPos}
      open={DrawerHOCstate[anchorPos]}
      sx={{ zIndex: 9999 }}
      onClose={toggleDrawer}
    >
      {list()}
    </DrawerHOC>
  );
}