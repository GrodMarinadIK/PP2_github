import datetime

class MickeyClockLogic:
    """
    Handles time-to-angle conversion for the clock hands.
    """
    def get_angles(self):
        now = datetime.datetime.now()
        
        # Calculate rotation angles based on 360-degree circle
        # Second hand: 6 degrees per second (360/60)
        sec_angle = now.second * 6
        
        # Minute hand: 6 degrees per minute + small offset for smooth movement
        min_angle = now.minute * 6 + now.second * 0.1
        
        # Hour hand: 30 degrees per hour (360/12) + offset based on current minutes
        hour_angle = (now.hour % 12) * 30 + now.minute * 0.5
        
        return sec_angle, min_angle, hour_angle