package edu.mbcai.pybootai.Controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @GetMapping("/")    //... Test OK
    public String Home() {
        return "index";    //... resources/templates/index.html을 찾아감
    }
}