import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ModalModule } from 'src/app/_modal/modal.module'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { OAComponent } from './oa/oa.component';
import { FormsModule , ReactiveFormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {ScrollingModule} from '@angular/cdk/scrolling';
import {CdkTableModule} from '@angular/cdk/table';
import {CdkTreeModule} from '@angular/cdk/tree';
import {MatButtonModule} from'@angular/material/button'
import {MatTableModule} from '@angular/material/table'
import {MatInputModule} from '@angular/material/input';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatTabsModule} from '@angular/material/tabs'
import {MatCardModule} from '@angular/material/card';
import { HelpComponent } from './help/help.component';

import { SplitterModule } from "primeng/splitter";
@NgModule({
  declarations: [
    AppComponent,
    OAComponent,
    HelpComponent
  ],
  imports: [ModalModule,
    SplitterModule,
    HttpClientModule,
    BrowserModule,
    MatTableModule,
    AppRoutingModule,
    MatInputModule,
    MatExpansionModule,
    MatTabsModule,
    MatCardModule,
    FormsModule,
    MatButtonModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
