package parse;

import java.util.HashMap;
import java.util.Map;

public class json_object implements value{
    private Map<String, value> map = new HashMap<>();
    private String name = null;

    public json_object(String _name){
        this.name = _name;
    }

    public void add(String str, value val){
        map.put(str , val);
    }

    public json_values getJSONValue(String key) {
        if(!map.containsKey(key)){
            return null;
        }
        value val = map.get(key);
        if (val instanceof json_values) {
            return (json_values) val;
        }
        System.out.println("JSONValue  \"" + key + "\" is not a JSONValue.");
        return null;
    }

    public json_array getJSONArray(String key) {
        if(!map.containsKey(key)){
            return null;
        }
        value val = map.get(key);
        if (val instanceof json_array) {
            return (json_array) val;
        }
        System.out.println("JSONArray  \"" + key + "\" is not a JSONArray.");
        return null;
    }

    public json_object getJSONObject(String key) {
        if(!map.containsKey(key)){
            return null;
        }
        value val = map.get(key);
        if (val instanceof json_object) {
            return (json_object) val;
        }
        System.out.println("JSONObject  \"" + key + "\" is not a JSONObject.");
        return null;
    }

    public String get_type(String key){
        if(!map.containsKey(key)){
            return null;
        }
        value val = map.get(key);
        if (val instanceof json_object) {
            return "obj";
        }else if (val instanceof json_array) {
            return "arr";
        }else if (val instanceof json_values) {
            return "val";
        }
        return null;
    }

    public value get_value(String _key){
        value val = null;
        String judge = get_type(_key);
        if(judge == "obj") {
            val = getJSONObject(_key);
        }else if(judge == "arr") {
            val = getJSONArray(_key);
        }else if(judge == "val") {
            val = getJSONValue(_key);
        }
        return val;
    }

    public String toString() {
        StringBuilder str = new StringBuilder();
        str.append("{ ");
        int size = map.size();
        for (String key : map.keySet()) {
            str.append(key + " : " + map.get(key).toString());
            if (--size != 0) {
                str.append(", ");
            }
        }
        str.append(" }");
        return str.toString();
    }
}
