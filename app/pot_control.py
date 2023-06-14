
def pot_status(plant:object, data:object):
    """
    Function that returns a string based on the values of sensor readings
    and values of the plant class
    @params
    plant - Plant class with values representing the plants preference for certain conditions. eg. temperature
    @params
    data - Data class representing the values of sensor readings
    """
    hidration_message="Hydration OK"
    pH_message="pH OK"
    temp_message="Temperature OK"
    light_message="Light OK"

    if plant.light == "High" and data.sen_light != "High":
        light_message="Light too low. Turning on lamp"

    if plant.light == "Mid" and data.sen_light == "Low":
        light_message="Light too low. Turning on lamp"   

    if plant.light == "Mid" and data.sen_light == "High":
        light_message="Light too high. Turning on shaders"

    if plant.light == "Low" and data.sen_light != "Low":
        light_message="Light too high. Turning on shaders"

    ###########################################################
    
    if plant.hydration == "High" and data.sen_hydration < 75:
        hidration_message = "Hydration too low. Starting watering"
        
    if plant.hydration == "Mid" and data.sen_hydration < 50:
        hidration_message = "Hydration too low. Starting watering"

    if plant.hydration == "Low" and data.sen_hydration < 25:
        hidration_message = "Hydration too low. Starting watering"

    ###########################################################

    if plant.pH == "High" and data.sen_pH < 10:
        pH_message = "Change soil"

    if plant.pH == "Mid" and (data.sen_pH < 6 or data.sen_pH > 8):
        pH_message = "Change soil"

    if plant.pH == "Low" and data.sen_pH > 5: 
        pH_message = "Change soil"
        
    ###########################################################

    if plant.warmth == "High" and data.sen_temp < 25:
        temp_message = "Temperature too low. Turning on heater"

    if plant.warmth == "Mid" and data.sen_temp > 25:
        temp_message = "Temperature too high. Turning on ventilation"
        
    if plant.warmth == "Mid" and data.sen_temp < 15:
        temp_message = "Temperature too low. Turning on heater"
    
    if plant.warmth == "Low" and data.sen_temp > 15:
        temp_message = "Temperature too high. Turning on ventilation"
    
    if plant.warmth == "Low" and data.sen_temp < 0:
        temp_message = "Temperature too low. Turning on heater"

    ###########################################################
    
    status = f"{temp_message}\n{hidration_message}\n{pH_message}\n{light_message}"
    #print(status)
    return status
   