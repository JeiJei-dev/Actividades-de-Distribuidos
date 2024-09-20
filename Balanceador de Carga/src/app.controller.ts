import { Controller, Get, Post } from "@nestjs/common";
import { AppService } from "./app.service";

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post("new-connection")
  async setNewConnection() {
    return this.appService.setNewConnection();
  }

  @Get("get-connections")
  async getConnections() {
    return this.appService.getUsers();
  }
}
