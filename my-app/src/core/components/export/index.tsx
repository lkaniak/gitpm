import Download from "@suid/icons-material/Download";
import { IconButton, Menu, MenuItem } from "@suid/material";
import { createSignal } from "solid-js";

export default function Export() {
  const [anchorEl, setAnchorEl] = createSignal<null | HTMLElement>(null);
  const open = () => Boolean(anchorEl());
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <IconButton
        id="download-button"
        color="secondary"
        aria-label="download"
        aria-controls={open() ? "basic-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open() ? "true" : undefined}
        onClick={(event) => {
          setAnchorEl(event.currentTarget);
        }}
      >
        <Download />
      </IconButton>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl()}
        open={open()}
        onClose={handleClose}
        MenuListProps={{ "aria-labelledby": "basic-button" }}
      >
        <MenuItem onClick={handleClose}>Log XES</MenuItem>
        <MenuItem onClick={handleClose}>Log CSV</MenuItem>
        <MenuItem onClick={handleClose}>Commits CSV</MenuItem>
      </Menu>
    </>
  );
}