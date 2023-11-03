class UserInterfaceCLI:
    def __init__(self, backend_service):
        self.backend_service = backend_service

    def display_menu(self):
        print("1. Option 1")
        print("2. Option 2")
        print("3. Exit")

    def get_user_choice(self):
        return input("Enter your choice: ")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            if choice == '1':
                print("You selected Option 1.")
                # Call some backend service method
                self.backend_service.method1()
            elif choice == '2':
                print("You selected Option 2.")
                # Call another backend service method
                self.backend_service.method2()
            elif choice == '3':
                print("Exiting.")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == '__main__':
    with open("config.json", "r") as file:
        config = json.load(file)
    backend_service = BackendService(config)
    ui = UserInterfaceCLI(backend_service)
    ui.run()