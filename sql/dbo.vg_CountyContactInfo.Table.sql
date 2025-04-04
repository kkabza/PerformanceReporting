USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_CountyContactInfo]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_CountyContactInfo](
	[CountyContactInfoID] [int] IDENTITY(1,1) NOT NULL,
	[VGProductCode] [int] NOT NULL,
	[DisplayContactInfo] [bit] NULL,
	[ContactName] [varchar](50) NULL,
	[ContactPhone] [varchar](50) NULL,
	[ContactFax] [varchar](50) NULL,
	[ContactEmail] [varchar](100) NULL,
	[MaillingAddressLine1] [varchar](50) NULL,
	[MailingAddressLine2] [varchar](50) NULL,
	[MailingAddressCity] [varchar](50) NULL,
	[MailingAddressState] [char](2) NULL,
	[MailingAddressZip] [varchar](10) NULL,
 CONSTRAINT [PK_vg_CountyContactInfo] PRIMARY KEY CLUSTERED 
(
	[CountyContactInfoID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
