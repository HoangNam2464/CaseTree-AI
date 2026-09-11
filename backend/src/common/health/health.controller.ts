import { Controller, Get } from "@nestjs/common";

@Controller("health")
export class HealthController {
  @Get()
  getHealth() {
    return {
      status: "UP",
      service: "EduBranch AI Backend Gateway",
      version: "1.0.0",
      framework: "NestJS",
      timestamp: new Date().toISOString(),
    };
  }
}
