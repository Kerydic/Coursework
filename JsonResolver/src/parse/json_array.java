package parse;

import java.util.ArrayList;
import java.util.List;

public class json_array implements value{
    private String array_name;
    private List<value> list = new ArrayList<>();

    public json_array(String name){
        this.array_name = name;
    }

    public String name(){
        return array_name;
    }

    public void add(value _value){
        list.add(_value);
    }

    public json_values getJSONValue(int key) {
        if(key>=list.size()){
            return null;
        }
        value val = list.get(key);
        if (val instanceof json_values) {
            return (json_values) val;
        }
        System.out.println("JSONArray[" + key + "] is not a JSONValue.");
        return null;
    }

    public json_array getJSONArray(int key) {
        if(key>=list.size()){
            return null;
        }
        value val = list.get(key);
        if (val instanceof json_array) {
            return (json_array) val;
        }
        System.out.println("JSONArray[" + key + "] is not a JSONArray.");
        return null;
    }

    public json_object getJSONObject(int key) {
        if(key>=list.size()){
            return null;
        }
        value val = list.get(key);
        if (val instanceof json_object) {
            return (json_object) val;
        }
        System.out.println("JSONArray[" + key + "] is not a JSONObject.");
        return null;
    }

    public String get_type(int key){
        if(key>=list.size()){
            return null;
        }
        value val = list.get(key);
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
        int key = Integer.parseInt(_key);
        String judge = get_type(key);
        if(judge == "obj") {
            val = getJSONObject(key);
        }else if(judge == "arr") {
            val = getJSONArray(key);
        }else if(judge == "val") {
            val = getJSONValue(key);
        }
        return val;
    }

    public int length(){
        return list.size();
    }

    public String toString(){
        StringBuilder str = new StringBuilder();
        str.append("[ ");
        for (int i =0; i < list.size(); i++) {
            str.append(list.get(i).toString());
            if (i != list.size() - 1) {
                str.append(", ");
            }
        }
        str.append(" ]");
        return str.toString();
    }
}
