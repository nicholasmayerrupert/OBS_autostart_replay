import obspython as obs

# default interval in seconds if not overridden
DEFAULT_INTERVAL = 60
interval = DEFAULT_INTERVAL


def script_description():
    return (
        "Keeps the replay buffer running by checking every interval and starting it if inactive. "
        "Requires the replay buffer to be enabled in Settings → Output. Adjust interval below."
    )


def script_properties():
    props = obs.obs_properties_create()
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
    global interval
    interval = obs.obs_data_get_int(settings, "interval")
    if interval < 1:
        interval = DEFAULT_INTERVAL
    obs.timer_remove(check_and_start)
    obs.timer_add(check_and_start, interval * 1000)
    print(f"[auto_replay_buffer] Interval set to {interval} seconds.")


def script_load(settings):
    # initialize timer (handles initial or saved settings)
    script_update(settings)


def script_unload():
    obs.timer_remove(check_and_start)
    print("[auto_replay_buffer] Unloaded: stopped monitoring.")


def check_and_start():
    # If the replay buffer is inactive, attempt to start it.
    if not obs.obs_frontend_replay_buffer_active():
        print("[auto_replay_buffer] Replay buffer inactive; attempting to start.")
        obs.obs_frontend_replay_buffer_start()
        # Immediately verify if it activated
        if obs.obs_frontend_replay_buffer_active():
            print("[auto_replay_buffer] Replay buffer started successfully.")
        else:
            print(
                "[auto_replay_buffer] Failed to start replay buffer. "
                "Make sure 'Enable Replay Buffer' is checked in Settings → Output."
            )
