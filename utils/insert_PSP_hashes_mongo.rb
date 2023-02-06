#!/opt/rubies/ruby-2.3.1/bin/ruby

# insert_PSP_hashes_mongo.rb

require_relative 'kannapedia_utils.rb'

Mongo::Logger.logger.level = Logger::FATAL

$DB = Mongo::Client.new([ENV["MONGO_HOST"]],
                   user: 'admin',
                   auth_source: 'admin',
                   password: ENV["ADMIN_PWORD"],
                   database: 'mgc_ss2_JL')