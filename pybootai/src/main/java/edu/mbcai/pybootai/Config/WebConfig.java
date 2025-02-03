package edu.mbcai.pybootai.Config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

//... Controller 역할 대행
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/ai").setViewName("ai");
    }    //... html page를 직접 요청할 수 있도록 View-Controller 설정 추가
    //... http://localhost:80/ai -> ai.html 파일 실행
}
