
require 'InputActivity'
require 'Log'

# Idle time threshold (in ms) - when do we assume the user was doing something else?
IDLE_TIME_THRESHOLD = (1000 * 60) * 15  # 15 minutes

# Set the current activity
def set_activity
  activity = get_next_activity

  # Log
  log_activity_now(get_last_activity)

  # Update current activity
  write_last_activity activity
end

set_activity
