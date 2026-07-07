let SHELLY_ID = "em";
Shelly.call("Mqtt.GetConfig", "", function (res, err_code, err_msg, ud) {
  SHELLY_ID = res["topic_prefix"];
});

function timerHandler(user_data)
{
  let em = Shelly.getComponentStatus("em1",2);
         MQTT.publish(SHELLY_ID + "/status/em1:2",
         JSON.stringify({"act_power":em.act_power,"current":em.current})
         ,0,false);
 }
Timer.set(1000, true, timerHandler, null);
