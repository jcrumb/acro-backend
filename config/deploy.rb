# config valid only for current version of Capistrano
lock '3.4.0'

set :application, 'acro'
set :repo_url, 'git@github.com:jcrumb/acro.git'

set :scm, :git

set :format, :pretty

set :log_level, :debug

set :pty, true


namespace :deploy do

  after :restart, :clear_cache do
    on roles(:api), in: :groups, limit: 3, wait: 10 do
      within release_path do
        execute "passenger-config restart-app /var/www/acro"
      end
    end
  end

end
