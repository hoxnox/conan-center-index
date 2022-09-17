#include <td/telegram/Client.h>
#include <td/telegram/td_api.h>
#include <td/telegram/td_api.hpp>

using namespace td;

int main(int argc, char *argv[])
{
	ClientManager::execute(td_api::make_object<td_api::setLogVerbosityLevel>(1));
	auto client_manager_ = std::make_unique<td::ClientManager>();
	auto client_id_ = client_manager_->create_client_id();
	client_manager_->send(client_id_, 1, td_api::make_object<td_api::getOption>("version"));
	return 0;
}
