import obspython as obs

# default interval in seconds if not overridden
DEFAULT_INTERVAL = 60
interval = DEFAULT_INTERVAL
enabled = True  # whether auto re-enabling is active


def script_description():
    return (
        "Automatically keeps the replay buffer running by periodically checking and re-enabling it if inactive. "
        "Requires the replay buffer to be enabled in Settings → Output. "
        "Toggle auto re-enabling below and adjust the check interval."
    )


def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "interval", DEFAULT_INTERVAL)
    obs.obs_data_set_default_bool(settings, "enabled", True)


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_bool(
        props,
        "enabled",
        "Enable auto re-enabling of the buffer",
    )
    obs.obs_properties_add_int(
        props,
        "interval",
        "Check interval (seconds)",
        5,
        3600,
        1,
    )
    return props


def script_update(settings):
    global interval, enabled
    interval = obs.obs_data_get_int(settings, "interval")
    if interval < 1:
        interval = DEFAULT_INTERVAL
    enabled = obs.obs_data_get_bool(settings, "enabled")
    obs.timer_remove(check_and_start)
    if enabled:
        obs.timer_add(check_and_start, interval * 1000)
        print(f"[auto_replay_buffer] Enabled auto re-enabling. Interval set to {interval} seconds.")
    else:
        print("[auto_replay_buffer] Disabled; auto re-enabling paused.")


def script_load(settings):
    # initialize timer (handles initial or saved settings)
    script_update(settings)


def script_unload():
    obs.timer_remove(check_and_start)
    print("[auto_replay_buffer] Unloaded: stopped monitoring.")


def check_and_start():
    if not enabled:
        return
    if not obs.obs_frontend_replay_buffer_active():
        print("[auto_replay_buffer] Replay buffer inactive; attempting to start.")
        obs.obs_frontend_replay_buffer_start()
        if obs.obs_frontend_replay_buffer_active():
            print("[auto_replay_buffer] Replay buffer re-enabled successfully.")
        else:
            print(
                "[auto_replay_buffer] Failed to re-enable replay buffer. "
                "Make sure 'Enable Replay Buffer' is checked in Settings → Output."
            )
